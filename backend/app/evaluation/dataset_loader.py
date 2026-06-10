from app.models import EvalDataset


def dataset_to_records(dataset: EvalDataset) -> list[dict]:
    return [question.model_dump() for question in dataset.questions]
