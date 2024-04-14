# Gradle Task Dependencies with Mermaid

This Python script uses the Gradle plugin `com.dorongold.task-tree` to calculate
the task dependencies of all tasks in a
[IntelliJ Platform Gradle Plugin](https://github.com/JetBrains/intellij-platform-gradle-plugin).
From this dependency tree, it calculates all edges between nodes and creates a 
[Mermaid FlowChart](https://mermaid.js.org/) string representation that can be rendered as an image like 
you find at the bottom.

# Usage

First, you need to have an IntelliJ Platform Plugin project that uses the IntelliJ Platform Gradle Plugin build setup.
You should have all tasks configured properly because otherwise, the dependency calculation will fail for
certain tasks.

Add the dependency to `taskTree` to your `plugins` section in `build.gradle.kts`

```
plugins {
    id("com.dorongold.task-tree") version "3.0.0"
}
```

Clone this repository and then call the following **from within** IntelliJ Plugin directory

```shell
python3 /path/to/mermaid_representation.py
```

At the moment, the Mermaid code will simply be printed to the console.
You can copy it and paste it the [Mermaid Live Editor](https://mermaid.live).

# Notes

The final graph layout depends on the order of the links between nodes. For now, I use
`MermaidRepresentation._sort_connections` to sort links `A --> B` by how often `B` appears on the left side
of a connection. This _seems_ to give a somewhat better layout.

Not all settings available are currently used properly. For example, the `mermaid_representation.TaskGroup` class
is supposed to collect similar tasks into `subgraph` boxes.
However, the definition of which tasks belong together needs to be discussed.
Additionally, the `mermaid_representation.MermaidStyle` gives another way of representing nodes that belong together
in the same style.
Again, it needs to be discussed which nodes belong to the same style group.

Finally, during the analysis, we will find connections of IntelliJ Platform Gradle Plugin
Tasks to core Gradle tasks, and it's not clear if we should show them or not.

# Example

Please also check the `examples` folder.

```mermaid
%%{init: {"flowchart": {"curve": "basis"}} }%%
flowchart BT



    subgraph BuildGroup["Build"]
         direction LR
         style BuildGroup fill:transparent
        buildPlugin:::buildStyle
        buildSearchableOptions:::buildStyle
        jarSearchableOptions:::buildStyle
        jarSearchableOptions --> buildSearchableOptions
        buildPlugin --> jarSearchableOptions
    end

    subgraph VerifyGroup["Verify"]
         direction LR
         style VerifyGroup fill:transparent
        verifyPluginSignature:::verifyStyle
        verifyPluginProjectConfiguration:::verifyStyle
        verifyPlugin:::verifyStyle
        verifyPluginStructure:::verifyStyle
    end

    subgraph GradleGroup["Gradle"]
         direction LR
         style GradleGroup fill:transparent
        classes:::gradleStyle
        compileJava:::gradleStyle
        testClasses:::gradleStyle
        processResources:::gradleStyle
        compileKotlin:::gradleStyle
        compileTestJava:::gradleStyle
        processTestResources:::gradleStyle
        compileJava --> compileKotlin
        compileTestJava --> classes
        classes --> processResources
        compileTestJava --> compileJava
        compileTestJava --> compileKotlin
        testClasses --> compileTestJava
        testClasses --> processTestResources
        classes --> compileJava
    end

    subgraph TestGroup["Test"]
         direction LR
         style TestGroup fill:transparent
        testIdeUi:::testStyle
        testIdePerformance:::testStyle
        prepareTest:::testStyle
        testIde:::testStyle
    end

    subgraph InstrumentationGroup["Instrumentation"]
         direction LR
         style InstrumentationGroup fill:transparent
        instrumentedJar:::instrumentStyle
        instrumentCode:::instrumentStyle
        instrumentedJar --> instrumentCode
    end

    subgraph PrintGroup["Print"]
         direction LR
         style PrintGroup fill:transparent
        printBundledPlugins:::printStyle
        printProductsReleases:::printStyle
    end

    subgraph RunGroup["Run"]
         direction LR
         style RunGroup fill:transparent
        runIde:::runStyle
    end

    subgraph PublishGroup["Publish"]
         direction LR
         style PublishGroup fill:transparent
        signPlugin:::publishStyle
        publishPlugin:::publishStyle
        publishPlugin --> signPlugin
    end

    subgraph PrepareGroup["Prepare"]
         direction LR
         style PrepareGroup fill:transparent
        prepareSandbox:::prepareStyle
        patchPluginXml:::prepareStyle
    end


    TestGroup --> GradleGroup
    VerifyGroup --> PrepareGroup
    RunGroup --> PrepareGroup
    BuildGroup --> PrepareGroup
    GradleGroup --> PrepareGroup
    PrepareGroup --> InstrumentationGroup
    TestGroup --> InstrumentationGroup
    PublishGroup --> BuildGroup
    VerifyGroup --> BuildGroup
    GradleGroup --> VerifyGroup
    TestGroup --> PrepareGroup
    GradleGroup --> InstrumentationGroup
    InstrumentationGroup --> GradleGroup

    classDef gradleStyle fill:#4285f4
    classDef runStyle fill:#b4ec51
    classDef instrumentStyle fill:#C1FF7A
    classDef buildStyle fill:#ffbe7b
    classDef publishStyle fill:#fff47d
    classDef prepareStyle fill:#FFFB7A
    classDef printStyle fill:#7AFFCE
    classDef testStyle fill:#4beee3
    classDef verifyStyle fill:#ff5e6c

    click runIde "#runIde"
    click printBundledPlugins "#printBundledPlugins"
    click prepareSandbox "#prepareSandbox"
    click printProductsReleases "#printProductsReleases"
    click verifyPluginSignature "#verifyPluginSignature"
    click verifyPluginProjectConfiguration "#verifyPluginProjectConfiguration"
    click verifyPlugin "#verifyPlugin"
    click testIdeUi "#testIdeUi"
    click buildPlugin "#buildPlugin"
    click testIdePerformance "#testIdePerformance"
    click instrumentedJar "#instrumentedJar"
    click signPlugin "#signPlugin"
    click buildSearchableOptions "#buildSearchableOptions"
    click prepareTest "#prepareTest"
    click jarSearchableOptions "#jarSearchableOptions"
    click publishPlugin "#publishPlugin"
    click patchPluginXml "#patchPluginXml"
    click instrumentCode "#instrumentCode"
    click verifyPluginStructure "#verifyPluginStructure"
    click testIde "#testIde"
```
