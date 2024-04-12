import subprocess
from typing import List


def run_gradle_task_tree(task: str) -> str:
    """
    This method runs a Gradle taskTree for a task specified by the `task` parameter and returns the output as a string.

    :param task: The name of the Gradle task to be used.
    :return: The output of the stdout running Gradle task execution as a string.
    """
    try:
        result = subprocess.run(
            ["./gradlew",
             "taskTree",
             "--no-configuration-cache",
             "--repeat",
             task], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode()
    except subprocess.CalledProcessError:
        raise RuntimeError(f"FAILED: Running Gradle taskTree with task '{task}' failed")


def parse_task_tree_output(task_name: str, output: str) -> List[tuple[str, int]]:
    """
    Takes the raw string output of the taskTree run and extracts the actual dependency-tree portion from it.
    :param task_name: The name of the task that was used.
    :param output: The output string from `run_gradle_task_tree`.
    :return: A list of tuples representing the task name and its respective level in the task tree.
    """
    lines = output.split("\n")
    dependencies = []
    state = 0
    whitespace_per_level = None
    for line in lines:
        if state == 0 and line.startswith(task_name):
            dependencies.append((task_name, 0))
            state = 1
        elif state == 1:
            if line == "":
                break
            index = line.index(":")
            if whitespace_per_level is None:
                whitespace_per_level = index
            dependencies.append((line[index:], index // whitespace_per_level))
    return dependencies


def do_collect_gradle_task_dependencies(task_level_info: List[tuple[str, int]]) -> set[tuple[str, str]]:
    result = set()
    task_stack = []
    current_level = 0
    for name, level in task_level_info:
        if level == 0:
            task_stack.append(name)
        elif level == current_level + 1:
            result.add((task_stack[-1], name))
            task_stack.append(name)
            current_level += 1
        elif level == current_level:
            task_stack.pop()
            result.add((task_stack[-1], name))
            task_stack.append(name)
        elif level < current_level:
            for _ in range(current_level - level + 1):
                task_stack.pop()
            result.add((task_stack[-1], name))
            task_stack.append(name)
            current_level = level
        else:
            print("Sheesh, that should not have happened!")
    return result


def collect_gradle_task_dependencies(task_name: str) -> set[tuple[str, str]]:
    try:
        task_output = run_gradle_task_tree(task_name)
        deps = parse_task_tree_output(task_name, task_output)
        return do_collect_gradle_task_dependencies(deps)
    except RuntimeError as e:
        print(e)
        return set()
