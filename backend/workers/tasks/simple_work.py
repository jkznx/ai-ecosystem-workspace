async def simple_work(ctx: dict, *args, **kwargs) -> dict:
    print(f"[simple_work] job_id={ctx.get('job_id')} args={args} kwargs={kwargs}")
    return {"job_id": ctx.get("job_id"), "args": args, "kwargs": kwargs}