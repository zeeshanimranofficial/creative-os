"""Creative OS v2 — Provider Layer (M4).

The OS is model-agnostic: generation happens through whichever top image
model the host agent runs. This layer therefore emits JOB CARDS — complete,
self-contained generation orders — and records results, so the pipeline is
auditable and replayable regardless of provider.

Flow: prompt_compiler -> JobCard -> (host agent generates; QA20b: open the
reference image with vision FIRST) -> record_result -> qa_engine -> retry_controller.
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS = os.path.join(ROOT, "registry", "jobs")


def new_job(compiled, dna_id, slide_id, out_path):
    """Write a job card the host agent executes with its image model.

    Args (all four required — documented contract, E2/FC-13):
        compiled:  dict returned by prompt_compiler.compile_prompt —
                   must carry 'prompt', 'reference_images', 'canvas'.
        dna_id:    the ONE approved DNA id this creative follows.
        slide_id:  stable slide identifier, e.g. 's03' (used in job_id).
        out_path:  where the host agent must save the generated raw.
    Returns: path of the written job-card JSON in registry/jobs/.
    """
    os.makedirs(JOBS, exist_ok=True)
    job = {
        "job_id": f"{slide_id}-{int(time.time())}",
        "slide_id": slide_id,
        "dna_id": dna_id,
        "status": "queued",
        "prompt": compiled["prompt"],
        "reference_images": compiled["reference_images"],
        "canvas": list(compiled["canvas"]),
        "output_path": out_path,
        "pre_gen_requirements": [
            "QA20b: re-open linked reference image(s) with vision before generating",
            "tombstone check already enforced by prompt_compiler",
        ],
        "post_gen_requirements": [
            "full-resolution copy-read of all rendered text",
            "run qa_engine numeric suite + vision tasks",
        ],
    }
    path = os.path.join(JOBS, job["job_id"] + ".json")
    with open(path, "w") as f:
        json.dump(job, f, indent=1)
    return path, job


def record_result(job_path, status, detail=""):
    """status: generated | qa_pass | qa_fail | regenerating | released | escalated"""
    with open(job_path) as f:
        job = json.load(f)
    job["status"] = status
    job.setdefault("history", []).append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "status": status, "detail": detail})
    with open(job_path, "w") as f:
        json.dump(job, f, indent=1)
    return job
