# prepareSandbox
```mermaid
%%{init: {"flowchart": {"curve": "basis"}} }%%
flowchart BT



    subgraph VerifyGroup["Verify"]
         direction LR
         style VerifyGroup fill:transparent
        verifyPluginProjectConfiguration:::verifyStyle
    end

    subgraph InstrumentationGroup["Instrumentation"]
         direction LR
         style InstrumentationGroup fill:transparent
        instrumentedJar:::instrumentStyle
        instrumentCode:::instrumentStyle
        instrumentedJar --> instrumentCode
    end

    subgraph PrepareGroup["Prepare"]
         direction LR
         style PrepareGroup fill:transparent
        prepareSandbox:::prepareStyle
        patchPluginXml:::prepareStyle
    end

    subgraph GradleGroup["Gradle"]
         direction LR
         style GradleGroup fill:transparent
        classes:::gradleStyle
        compileJava:::gradleStyle
        compileKotlin:::gradleStyle
        processResources:::gradleStyle
        compileJava --> compileKotlin
        classes --> processResources
        classes --> compileJava
    end


        compileJava --> verifyPluginProjectConfiguration
        verifyPluginProjectConfiguration --> patchPluginXml
        instrumentedJar --> classes
        instrumentCode --> classes
        instrumentedJar --> compileJava
        instrumentedJar --> compileKotlin
        prepareSandbox --> instrumentedJar
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

    click instrumentedJar "#instrumentedJar"
    click prepareSandbox "#prepareSandbox"
    click verifyPluginProjectConfiguration "#verifyPluginProjectConfiguration"
    click instrumentCode "#instrumentCode"
    click patchPluginXml "#patchPluginXml"
```
