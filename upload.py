from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_ingestion import save_upload_to_disk, read_dataframe, sample_preview
from app.services.profiling import quick_profile

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        saved_path = save_upload_to_disk(file_bytes, file.filename)
        df = read_dataframe(saved_path)
        profile = quick_profile(df)
        preview = sample_preview(df, n=20)
        return {
            "dataset_path": str(saved_path),  # for now; later switch to an ID
            "profile": profile,
            "preview": preview,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")