
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.data_manager import DataManager
from app.core.task_processor import TaskProcessor
from app.utils.logging import logger

router = APIRouter()
data_manager = DataManager()
task_processor = TaskProcessor(data_manager)

class TransformRequest(BaseModel):
    column: str
    transform_type: str
    parameters: dict = {}

@router.post("/load_dataset")
async def load_dataset(file: UploadFile = File(...)):
    """Upload and load a CSV dataset."""
    if not file.filename.endswith(".csv"):
        logger.error("Invalid file format: must be CSV")
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    result = data_manager.load(file.file)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    analysis = data_manager.analyze_columns()
    preview = data_manager.preview()
    return {
        "status": "success",
        "message": "Dataset loaded and analyzed",
        "column_groups": analysis["data"],
        "preview": preview["data"]
    }

@router.post("/apply_transform")
async def apply_transform(request: TransformRequest):
    """Apply a transformation to a column based on drag-and-drop."""
    transform_type = request.transform_type
    column = request.column
    parameters = request.parameters

    if transform_type == "fillna":
        strategy = parameters.get("strategy", "mean")
        result = task_processor.fillna(column, strategy)
    elif transform_type == "convert_to_numerical":
        result = task_processor.convert_to_numerical(column)
    elif transform_type == "convert_to_categorical":
        result = task_processor.convert_to_categorical(column)
    else:
        logger.error(f"Invalid transform type: {transform_type}")
        raise HTTPException(status_code=400, detail="Invalid transform type")

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    analysis = data_manager.analyze_columns()
    preview = data_manager.preview()
    return {
        "status": "success",
        "message": result["message"],
        "column_groups": analysis["data"],
        "preview": preview["data"]
    }

@router.get("/get_preview")
async def get_preview():
    """Get a preview of the current DataFrame."""
    result = data_manager.preview()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/save_dataset")
async def save_dataset():
    """Save the current DataFrame to a CSV file."""
    result = data_manager.save()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return FileResponse(result["file"], media_type="text/csv", filename="output.csv")

@router.post("/reset")
async def reset():
    """Reset the DataFrame and history."""
    result = data_manager.reset()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result