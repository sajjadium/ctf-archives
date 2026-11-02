by Hidden Investigations
hardware
A satellite ground-support station runs its propellant fueling and cooling on an aging GSC-7 field controller. Before the next payload test can be authorized, the controller has to be validated — and right now it won't pass: a safety interlock on the fueling sequence looks wrong, and the one engineer who touched it last is unreachable.

You're the contracted security engineer. You have network access to the live controller and a copy of its maintenance toolkit, including the controller firmware image. Work out how the controller authenticates an engineer, find and correct the altered safety logic, make the fix actually stick, and bring the fueling/cooling test to a clean, safe completion. The controller issues a validation token only on a genuinely successful run.

This is a facility-validation exercise: defensive work on launch-support infrastructure. No targeting or weapons systems are involved.

The toolkit, firmware image, protocol reference, and control narrative are in the download. The controller exposes a control service and a read-only telemetry feed; see the reference document for ports and commands.
