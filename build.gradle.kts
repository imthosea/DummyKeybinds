fun properties(key: String) = providers.gradleProperty(key)

plugins {
    id("java")
    id("org.jetbrains.intellij").version("1.17.2")
}

group = "me.thosea"
version = properties("version")

repositories {
    mavenCentral()
}

intellij {
    pluginName = properties("pluginName")
    version = properties("platformVersion")
}

tasks {
    wrapper {
        gradleVersion = properties("gradleVersion").get()
    }

    patchPluginXml {
        version = properties("version")
        sinceBuild = properties("pluginSinceBuild")
    }
}