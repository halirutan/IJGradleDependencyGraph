# compileJava
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
        compileJava:::gradleStyle
        compileJava --> compileKotlin
    end

    subgraph PrepareGroup["Prepare"]
         direction LR
         style PrepareGroup fill:transparent
        patchPluginXml:::prepareStyle
    end


        verifyPluginProjectConfiguration --> patchPluginXml
        compileJava --> verifyPluginProjectConfiguration
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
    click patchPluginXml "#patchPluginXml"
```
