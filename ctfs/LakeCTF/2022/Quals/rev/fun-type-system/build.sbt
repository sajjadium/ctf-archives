val scala3Version = "3.1.3"

lazy val root = project
  .in(file("."))
  .settings(
    name := "fun-type-system",
    version := "1.0.0",

    scalaVersion := scala3Version,
  )
