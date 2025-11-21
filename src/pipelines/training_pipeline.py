from prefect import flow, task
from src.data.download_data import download_data
from src.data.process_data import process_data
from src.models.train import train

@task
def task_download_data():
    download_data()

@task
def task_process_data():
    process_data()

@task
def task_train_model(n_estimators: int = 100, max_depth: int = None):
    train(n_estimators=n_estimators, max_depth=max_depth)

@flow(name="Predictive Maintenance Training Flow")
def training_flow(n_estimators: int = 100, max_depth: int = None):
    task_download_data()
    task_process_data()
    task_train_model(n_estimators=n_estimators, max_depth=max_depth)

if __name__ == "__main__":
    training_flow()
