# runIde
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

    subgraph GradleGroup["Gradle"]
         direction LR
         style GradleGroup fill:transparent
        compileJava:::gradleStyle
        classes:::gradleStyle
        compileKotlin:::gradleStyle
        processResources:::gradleStyle
        compileJava --> compileKotlin
        classes --> processResources
        classes --> compileJava
    end

    subgraph RunGroup["Run"]
         direction LR
         style RunGroup fill:transparent
        runIde:::runStyle
    end

    subgraph PrepareGroup["Prepare"]
         direction LR
         style PrepareGroup fill:transparent
        prepareSandbox:::prepareStyle
        patchPluginXml:::prepareStyle
    end


        compileJava --> verifyPluginProjectConfiguration
        runIde --> prepareSandbox
        runIde --> patchPluginXml
        verifyPluginProjectConfiguration --> patchPluginXml
        processResources --> patchPluginXml
        instrumentedJar --> classes
        instrumentCode --> classes
        instrumentedJar --> compileKotlin
        prepareSandbox --> instrumentedJar
        instrumentedJar --> compileJava
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
    click runIde "#runIde"
    click prepareSandbox "#prepareSandbox"
    click verifyPluginProjectConfiguration "#verifyPluginProjectConfiguration"
    click instrumentCode "#instrumentCode"
    click patchPluginXml "#patchPluginXml"
```
