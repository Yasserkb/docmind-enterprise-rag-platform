from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.schemas import CreateDatasetRequest, CreateEvalRunRequest
from app.evaluation.comparison import compare_runs
from app.evaluation.runner import EvaluationRunner
from app.models import EvalDataset, EvalRun
from app.storage.store import store

router = APIRouter(prefix="/eval", tags=["evaluation"])


@router.post("/datasets", response_model=EvalDataset)
def create_dataset(req: CreateDatasetRequest) -> EvalDataset:
    if req.collection_id not in store.collections:
        raise HTTPException(404, "Collection not found")
    dataset = EvalDataset(**req.model_dump())
    store.eval_datasets[dataset.id] = dataset
    return dataset


@router.get("/datasets", response_model=list[EvalDataset])
def list_datasets() -> list[EvalDataset]:
    return list(store.eval_datasets.values())


@router.post("/runs", response_model=EvalRun)
def start_eval(req: CreateEvalRunRequest) -> EvalRun:
    if req.dataset_id not in store.eval_datasets:
        raise HTTPException(404, "Dataset not found")
    run = EvalRun(**req.model_dump())
    store.eval_runs[run.id] = run
    return EvaluationRunner(store).run(run)


@router.get("/runs", response_model=list[EvalRun])
def list_eval_runs() -> list[EvalRun]:
    return list(store.eval_runs.values())


@router.get("/runs/{run_id}", response_model=EvalRun)
def get_eval_run(run_id: UUID) -> EvalRun:
    if run_id not in store.eval_runs:
        raise HTTPException(404, "Evaluation run not found")
    return store.eval_runs[run_id]


@router.post("/runs/compare")
def compare_eval_runs(run_a: UUID, run_b: UUID) -> dict:
    first, second = store.eval_runs.get(run_a), store.eval_runs.get(run_b)
    if not first or not second:
        raise HTTPException(404, "Both runs must exist")
    return compare_runs(first, second)
