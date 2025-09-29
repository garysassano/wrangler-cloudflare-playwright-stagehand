import { Stagehand } from "@browserbasehq/stagehand";
import { endpointURLString } from "@cloudflare/playwright";
import { z } from "zod";
import { WorkersAIClient } from "./workersAIClient";

export default {
  async fetch(request: Request, env: Env) {
    if (new URL(request.url).pathname !== "/") return new Response("Not found", { status: 404 });

    const stagehand = new Stagehand({
      env: "LOCAL",
      localBrowserLaunchOptions: { cdpUrl: endpointURLString(env.BROWSER) },
      llmClient: new WorkersAIClient(env.AI),
      verbose: 1,
    });

    await stagehand.init();
    const page = stagehand.page;

    await page.goto("https://demo.playwright.dev/movies");

    // if search is a multi-step action, stagehand will return an array of actions it needs to act on
    const actions = await page.observe('Search for "Furiosa"');
    for (const action of actions) await page.act(action);

    await page.act("Click the search result");

    // normal playwright functions work as expected
    await page.waitForSelector(".info-wrapper .cast");

    const movieInfo = await page.extract({
      instruction: "Extract movie information",
      schema: z.object({
        title: z.string(),
        year: z.number(),
        rating: z.number(),
        genres: z.array(z.string()),
        duration: z.number().describe("Duration in minutes"),
      }),
    });

    await stagehand.close();

    return Response.json(movieInfo);
  },
};
