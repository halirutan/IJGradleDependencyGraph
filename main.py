from config import Config
from task_analysis import collect_all_gradle_task_dependencies
from mermaid_representation import MermaidRepresentation


def save_markdown_file(file: str, title: str, mermaid_code: str) -> None:
    content = "\n".join(
        ["# " + title] +
        ["```mermaid"] +
        [mermaid_code] +
        ["```\n"]
    )
    with open(file, "w") as f:
        f.write(content)


def main():
    config = Config()
    dependencies, excluded = collect_all_gradle_task_dependencies(config)
    mermaid = MermaidRepresentation(dependencies, config)

    # Create a dependency graph for each task
    for task in config.included_task_map.keys():
        mermaid_representation = mermaid.mermaid_representation_single_task(task)
        task_name = config.get_task_identifier(task)
        save_markdown_file(f"{task_name}_graph.md", task_name, mermaid_representation)

    # Create an overview of all dependencies but group tasks into categories
    overview = mermaid.mermaid_representation_all_tasks()
    save_markdown_file("overview_grouped_graph.md", "Overview All Tasks Grouped", overview)

    # Create an overview of all dependencies without grouping
    overview = mermaid.mermaid_representation_all_tasks(grouped=False)
    save_markdown_file("overview_ungrouped_graph.md", "Overview All Tasks", overview)

    with open("mermaid_excluded_tasks.txt", "w") as f:
        for e in sorted(excluded):
            f.write(f"{e}\n")


if __name__ == '__main__':
    main()
