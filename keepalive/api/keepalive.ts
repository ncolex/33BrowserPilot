export const config = {
  runtime: 'edge',
};

export default async function handler(request: Request) {
  const HF_SPACE_URL = process.env.HF_SPACE_URL;

  if (!HF_SPACE_URL) {
    return new Response(
      JSON.stringify({ error: 'HF_SPACE_URL not configured' }),
      { status: 500, headers: { 'content-type': 'application/json' } }
    );
  }

  try {
    console.log(`🔍 Pinging Hugging Face Space: ${HF_SPACE_URL}`);
    
    const response = await fetch(HF_SPACE_URL, {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; KeepAliveBot/1.0)',
      },
    });

    const status = response.status;
    const ok = status >= 200 && status < 400;

    console.log(`✅ Ping result: ${status} ${ok ? 'OK' : 'ERROR'}`);

    return new Response(
      JSON.stringify({
        success: ok,
        status: status,
        url: HF_SPACE_URL,
        timestamp: new Date().toISOString(),
      }),
      {
        status: ok ? 200 : 500,
        headers: { 'content-type': 'application/json' },
      }
    );
  } catch (error: any) {
    console.error('❌ Ping failed:', error.message);
    
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
        url: HF_SPACE_URL,
        timestamp: new Date().toISOString(),
      }),
      {
        status: 500,
        headers: { 'content-type': 'application/json' },
      }
    );
  }
}
