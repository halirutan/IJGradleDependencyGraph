from dataclasses import dataclass


@dataclass
class MermaidStyle:
    """Style definition used to style a class of nodes"""
    identifier: str
    """Name of the style class"""
    class_def: str
    """Style definition, e.g. 'fill:#ff5e6c'"""

    @property
    def class_def(self):
        return f"classDef {self.identifier} {self._class_def}"

    @class_def.setter
    def class_def(self, value):
        # Your setter implementation goes here
        self._class_def = value


@dataclass
class TaskGroup:
    """Currently not used"""
    identifier: str = "DEFAULT"
    name: str = "default"


@dataclass
class IntelliJTask:
    """Represents one Task of the IntelliJ Gradle Plugin"""
    name: str
    """Name with leading :"""
    style_group: MermaidStyle
    """Style used for this node in Mermaid"""
    task_group: TaskGroup
    """Currently not used"""


verifyStyle = MermaidStyle("verifyStyle", "fill:#ff5e6c")
buildStyle = MermaidStyle("buildStyle", "fill:#ffbe7b")
publishStyle = MermaidStyle("publishStyle", "fill:#fff47d")
runStyle = MermaidStyle("runStyle", "fill:#b4ec51")
testStyle = MermaidStyle("testStyle", "fill:#4beee3")
gradleStyle = MermaidStyle("gradleStyle", "fill:#4285f4")


class MermaidRepresentation:
    intellj_gradle_plugin_tasks = [
        IntelliJTask(":buildPlugin", buildStyle, TaskGroup()),
        IntelliJTask(":buildSearchableOptions", buildStyle, TaskGroup()),
        IntelliJTask(":initializeIntellijPlatformPlugin", buildStyle, TaskGroup()),
        IntelliJTask(":instrumentCode", buildStyle, TaskGroup()),
        IntelliJTask(":instrumentTestCode", buildStyle, TaskGroup()),
        IntelliJTask(":jarSearchableOptions", buildStyle, TaskGroup()),
        IntelliJTask(":patchPluginXml", buildStyle, TaskGroup()),
        IntelliJTask(":prepareSandbox", buildStyle, TaskGroup()),
        IntelliJTask(":prepareTestSandbox", buildStyle, TaskGroup()),
        IntelliJTask(":prepareUiTestSandbox", buildStyle, TaskGroup()),
        IntelliJTask(":printBundledPlugins", buildStyle, TaskGroup()),
        IntelliJTask(":printProductsReleases", buildStyle, TaskGroup()),
        IntelliJTask(":publishPlugin", publishStyle, TaskGroup()),
        IntelliJTask(":runIde", runStyle, TaskGroup()),
        IntelliJTask(":signPlugin", publishStyle, TaskGroup()),
        IntelliJTask(":testIdePerformance", testStyle, TaskGroup()),
        IntelliJTask(":testIdeUi", testStyle, TaskGroup()),
        IntelliJTask(":verifyPlugin", verifyStyle, TaskGroup()),
        IntelliJTask(":verifyPluginProjectConfiguration", verifyStyle, TaskGroup()),
        IntelliJTask(":verifyPluginSignature", verifyStyle, TaskGroup()),
        IntelliJTask(":verifyPluginStructure", verifyStyle, TaskGroup()),
    ]

    mermaid_prefix = """
    %%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%

    flowchart BT
    
    """.lstrip()

    @staticmethod
    def _sort_connections(connections: set[tuple[str, str]]) -> list[tuple[str, str]]:
        """
        Sorts the connections `A --> B` based on the count of B's in all connections.

        :param connections: A set of tuples representing connections.
        :return: A sorted list of tuples representing connections.
        """
        values = [x[1] for x in connections]
        sorting_count = {x: values.count(x) for x in values}
        return sorted(connections, key=lambda x: sorting_count[x[1]])

    @staticmethod
    def create_mermaid_representation() -> str:
        import task_analysis
        dependencies = set()
        node_definitions = {}
        for task in MermaidRepresentation.intellj_gradle_plugin_tasks:
            node_definitions[task.name] = f"    {task.name[1:]}:::{task.style_group.identifier}"
            print(f"Calculating dependencies of task '{task.name}'")
            dependencies = dependencies.union(task_analysis.collect_gradle_task_dependencies(task.name))
        node_connections = []
        for edge in MermaidRepresentation._sort_connections(dependencies):
            if edge[1] not in node_definitions:
                node_definitions[edge[1]] = f"    {edge[1][1:]}:::{gradleStyle.identifier}"
            if True or edge[1] != ":initializeIntellijPlatformPlugin":
                node_connections.append(f"    {edge[0][1:]} --> {edge[1][1:]}")
        node_connections.append("")
        return "\n".join(
            [MermaidRepresentation.mermaid_prefix] +
            list(node_definitions.values()) +
            node_connections +
            [f"    {x.class_def}" for x in [verifyStyle, buildStyle, publishStyle, runStyle, testStyle, gradleStyle]]
        )


if __name__ == '__main__':
    mermaid_result = MermaidRepresentation().create_mermaid_representation()
    print("\n\n")
    print(mermaid_result)
