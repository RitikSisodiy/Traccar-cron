export const dynamic = 'force-dynamic';

async function pingWebsite(url: string): Promise<boolean> {
  try {
    const response = await fetch(url, { method: 'GET' });
    if (response.ok) {
      console.log("Website is up.");
      return true;
    } else {
      console.log(`Unexpected status code: ${response.status}`);
      return false;
    }
  } catch (error) {
    console.error(`Error accessing website: ${error}`);
    return false;
  }
}

async function restartService(): Promise<Response> {
  const apiToken = process.env.RENDER_API_TOKEN;
  const serviceId = process.env.SERVICE_ID;

  if (!apiToken || !serviceId) {
    return new Response("Environment variables RENDER_API_TOKEN and SERVICE_ID must be set.", { status: 500 });
  }

  try {
    const response = await fetch(`https://api.render.com/v1/services/${serviceId}/deploys`, {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'authorization': `Bearer ${apiToken}`,
        'content-type': 'application/json'
      }
    });

    if (response.ok) {
      console.log("Service restart triggered successfully.");
      const data = await response.json();
      return new Response(`Service restarted successfully: ${JSON.stringify(data)}`);
    } else {
      const errorData = await response.text();
      console.error("Failed to trigger service restart:", errorData);
      return new Response(`Failed to trigger service restart. Status: ${response.status}`, { status: response.status });
    }
  } catch (error) {
    console.error("Error occurred during service restart:", error);
    return new Response(`Error occurred during service restart: ${error}`, { status: 500 });
  }
}

export async function GET(request: Request): Promise<Response> {
  const websiteURL = 'https://traccer.onrender.com/healthcheck';

  const isWebsiteUp = await pingWebsite(websiteURL);
  if (!isWebsiteUp) {
    console.log("Website is down. Restarting service...");
    return await restartService();
  }

  return new Response("Website is up. No restart needed.");
}
