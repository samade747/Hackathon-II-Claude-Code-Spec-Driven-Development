import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.todo.models import Task
from src.todo.storage import InMemoryStorage
from src.todo.utils import now_iso

def run_demo():
    print("🚀 Starting Todo App Logic Demo (In-Memory Persistence)")
    print("======================================================\n")

    storage = InMemoryStorage()

    # 1. Add Tasks
    print("1️⃣  Adding Tasks...")
    task1 = Task(title="Buy Groceries", description="Milk, Eggs, Bread", priority="high", tags=["shopping"])
    task2 = Task(title="Walk the Dog", priority="medium", tags=["personal"])
    task3 = Task(title="Finish Project", description="Coding implementation", priority="high", tags=["work"], due_date="2025-12-12T10:00:00Z")
    
    storage.add_task(task1)
    storage.add_task(task2)
    storage.add_task(task3)
    
    print(f"✅ Added 3 tasks.\n")

    # 2. List Tasks
    print("2️⃣  Listing All Tasks:")
    tasks = storage.list_tasks()
    for t in tasks:
        print(f"   - [{t.status.upper()}] {t.title} (Priority: {t.priority})")
    print("")

    # 3. Search Tasks
    print("3️⃣  Searching for 'work' tags:")
    results = storage.search_tasks(tags=["work"])
    for t in results:
        print(f"   - Found: {t.title}")
    print("")

    # 4. Update Task
    print(f"4️⃣  Updating '{task2.title}'...")
    storage.update_task(task2.id, title="Walk the Dog (Long Walk)", priority="high")
    updated_task2 = storage.get_task(task2.id)
    print(f"   - New Title: {updated_task2.title}")
    print(f"   - New Priority: {updated_task2.priority}\n")

    # 5. Complete Task
    print(f"5️⃣  Completing '{task1.title}'...")
    storage.update_task(task1.id, status="completed")
    completed_task1 = storage.get_task(task1.id)
    print(f"   - Status is now: {completed_task1.status}\n")

    # 6. Delete Task
    print(f"6️⃣  Deleting '{task3.title}'...")
    storage.delete_task(task3.id)
    remaining = storage.list_tasks()
    print(f"   - Remaining tasks count: {len(remaining)}\n")

    print("🎉 Demo Completed Successfully!")

if __name__ == "__main__":
    run_demo()
