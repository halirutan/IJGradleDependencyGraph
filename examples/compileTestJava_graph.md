# compileTestJava
```mermaid
%%{init: {"flowchart": {"curve": "basis"}} }%%
flowchart BT



    subgraph VerifyGroup["Verify"]
         direction LR
         style VerifyGroup fill:transparent
        verifyPluginProjectConfiguration:::verifyStyle
    end

    subgraph GradleGroup["Gradle"]
         direction LR
         style GradleGroup fill:transparent
        compileKotlin:::gradleStyle
        classes:::gradleStyle
        compileJava:::gradleStyle
        compileTestJava:::gradleStyle
        processResources:::gradleStyle
        compileTestJava --> compileJava
        compileJava --> compileKotlin
        classes --> processResources
        compileTestJava --> compileKotlin
        compileTestJava --> classes
        classes --> compileJava
    end

    subgraph PrepareGroup["Prepare"]
         direction LR
         style PrepareGroup fill:transparent
        patchPluginXml:::prepareStyle
    end

    subgraph InstrumentationGroup["Instrumentation"]
         direction LR
         style InstrumentationGroup fill:transparent
        instrumentCode:::instrumentStyle
    end


        compileJava --> verifyPluginProjectConfiguration
        verifyPluginProjectConfiguration --> patchPluginXml
        compileTestJava --> instrumentCode
        instrumentCode --> classes
        compileTestJava --> verifyPluginProjectConfiguration
        processResources --> patchPluginXml
        compileKotlin --> verifyPluginProjectConfiguration

    classDef gradleStyle fill:#4285f4
    classDef runStyle fill:#b4ec51
    classDef instrumentStyle fill:#C1FF7A
    classDef buildStyle fill:#ffbe7b
    classDef publishStyle fill:#fff47d
    classDef prepareStyle fill:#FFFB7A
    classDef printStyle fill:#7AFFCE
    classDef testStyle fill:#4beee3
    classDef verifyStyle fill:#ff5e6c

    click verifyPluginProjectConfiguration "#verifyPluginProjectConfiguration"
    click instrumentCode "#instrumentCode"
    click patchPluginXml "#patchPluginXml"
```
