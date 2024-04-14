from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class MermaidClassStyle:
    """Style definition used to style a class of nodes"""
    identifier: Optional[str] = None
    """Name of the style class"""
    style_definition: Optional[str] = None
    """Style definition, e.g. 'fill:#ff5e6c'"""

    @property
    def class_def(self) -> str:
        if self.identifier is None or self.style_definition is None:
            return ""
        return f"classDef {self.identifier} {self.style_definition}"


@dataclass(frozen=True)
class TaskGroup:
    """Helps to put tasks into similar groups"""
    identifier: Optional[str] = None
    name: Optional[str] = None


buildGroup = TaskGroup("BuildGroup", "Build")
gradleGroup = TaskGroup("GradleGroup", "Gradle")
runGroup = TaskGroup("RunGroup", "Run")
instrumentGroup = TaskGroup("InstrumentationGroup", "Instrumentation")
prepareGroup = TaskGroup("PrepareGroup", "Prepare")
publishGroup = TaskGroup("PublishGroup", "Publish")
testGroup = TaskGroup("TestGroup", "Test")
verifyGroup = TaskGroup("VerifyGroup", "Verify")
printGroup = TaskGroup("PrintGroup", "Print")


@dataclass
class GradleTask:
    """Represents one Task of the IntelliJ Gradle Plugin"""
    name: str
    """Name with leading :"""
    style: MermaidClassStyle = MermaidClassStyle()
    """Style used for this node in Mermaid"""
    task_group: TaskGroup = TaskGroup()
    """Currently not used"""
    has_url_anchor: bool = False
    """If set to true, we add a click listener to the node that links to an anchor with the same name as the task."""


verifyStyle = MermaidClassStyle("verifyStyle", "fill:#ff5e6c")
buildStyle = MermaidClassStyle("buildStyle", "fill:#ffbe7b")
instrumentStyle = MermaidClassStyle("instrumentStyle", "fill:#C1FF7A")
prepareStyle = MermaidClassStyle("prepareStyle", "fill:#FFFB7A")
publishStyle = MermaidClassStyle("publishStyle", "fill:#fff47d")
runStyle = MermaidClassStyle("runStyle", "fill:#b4ec51")
testStyle = MermaidClassStyle("testStyle", "fill:#4beee3")
gradleStyle = MermaidClassStyle("gradleStyle", "fill:#4285f4")
printStyle = MermaidClassStyle("printStyle", "fill:#7AFFCE")


class Config:
    included_tasks = [
        GradleTask(":buildPlugin", buildStyle, buildGroup, True),
        GradleTask(":buildSearchableOptions", buildStyle, buildGroup, True),
        GradleTask(":instrumentCode", instrumentStyle, instrumentGroup, True),
        GradleTask(":instrumentedJar", instrumentStyle, instrumentGroup, True),
        GradleTask(":jarSearchableOptions", buildStyle, buildGroup, True),
        GradleTask(":patchPluginXml", prepareStyle, prepareGroup, True),
        GradleTask(":prepareSandbox", prepareStyle, prepareGroup, True),
        GradleTask(":printBundledPlugins", printStyle, printGroup, True),
        GradleTask(":printProductsReleases", printStyle, printGroup, True),
        GradleTask(":publishPlugin", publishStyle, publishGroup, True),
        GradleTask(":runIde", runStyle, runGroup, True),
        GradleTask(":signPlugin", publishStyle, publishGroup, True),
        GradleTask(":prepareTest", testStyle, testGroup, True),
        GradleTask(":testIde", testStyle, testGroup, True),
        GradleTask(":testIdePerformance", testStyle, testGroup, True),
        GradleTask(":testIdeUi", testStyle, testGroup, True),
        GradleTask(":verifyPlugin", verifyStyle, verifyGroup, True),
        GradleTask(":verifyPluginProjectConfiguration", verifyStyle, verifyGroup, True),
        GradleTask(":verifyPluginSignature", verifyStyle, verifyGroup, True),
        GradleTask(":verifyPluginStructure", verifyStyle, verifyGroup, True),
        GradleTask(":classes", gradleStyle, gradleGroup),
        GradleTask(":compileJava", gradleStyle, gradleGroup),
        GradleTask(":compileKotlin", gradleStyle, gradleGroup),
        GradleTask(":compileTestJava", gradleStyle, gradleGroup),
        # GradleTask(":initializeIntellijPlatformPlugin", gradleStyle, TaskGroup()),
        # GradleTask(":patchChangelog", gradleStyle, ),
        GradleTask(":processResources", gradleStyle, gradleGroup),
        GradleTask(":processTestResources", gradleStyle, gradleGroup),
        GradleTask(":testClasses", gradleStyle, gradleGroup)
    ]

    def __init__(self):
        self.included_task_map = {t.name: t for t in Config.included_tasks}

    def is_included_task(self, task_name: str) -> bool:
        return task_name in self.included_task_map.keys()

    def get_task_style(self, task_name: str) -> MermaidClassStyle:
        assert self.is_included_task(task_name)
        return self.included_task_map[task_name].style

    def get_task_click_anchor(self, task_name: str) -> str:
        assert self.is_included_task(task_name)
        if self.included_task_map[task_name].has_url_anchor:
            name = self.get_task_identifier(task_name)
            return f"    click {name} \"#{name}\""
        else:
            return ""

    def get_task_group(self, task_name: str) -> TaskGroup:
        assert self.is_included_task(task_name)
        return self.included_task_map[task_name].task_group

    def get_task_identifier(self, task_name) -> str:
        assert self.is_included_task(task_name)
        return task_name[1:]

    def get_all_style_definitions(self) -> List[str]:
        all_styles = {s.style for s in self.included_task_map.values()}
        return [f"    {x.class_def}" for x in all_styles]

    def get_all_click_anchors(self) -> List[str]:
        all_anchors = {self.get_task_identifier(a.name) for a in self.included_task_map.values() if a.has_url_anchor}
        return [f"    click {x} \"#{x}\"" for x in all_anchors]
