import { device } from "@shared/device";
import { column, render, type Node } from "@busy-app/busy-lib";
import manifest from "./appmeta/manifest.json";

// The name the app draws under; the device clears elements by this id.
const APP = manifest.id;

let stopped = false;

// The frame drawn on every tick. The screen is 72×16, so two short lines are about all that fits.
function frame(): Node
{
  return column({justify: "center", align: "center"}, [{type: "animation", id: "0", width: 72, height: 16, path: "animations/nemo.anim", loop: true}]);
}

// Sends one frame to the device.
async function draw(): Promise<void>
{
  const elements = render(frame());
  await device.DisplayDraw({application_name: APP, priority: 50, elements});
}

// Entry point, called at the end of the file: the device runs this script from top to bottom and starts nothing by itself.
function main(): void
{
  const report = (err: unknown) => console.error(`${APP}: ${err instanceof Error ? err.message : String(err)}`);

  void draw().catch(report);

  const unbind = listen("input", (event) =>
  {
    if (stopped || event.key !== "back" || event.action !== "short")
    {
      return;
    }

    stopped = true;

    // Not detached from inside the handler itself: with nothing else left the unbind stops the app on the spot, while this handler is still running.
    setTimeout(unbind, 0);
  });
}
main();
