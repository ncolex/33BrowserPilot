const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const HF_SPACE_URL = process.env.HF_SPACE_URL;

  if (!HF_SPACE_URL) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'HF_SPACE_URL not configured' }),
    };
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

    return {
      statusCode: ok ? 200 : 500,
      body: JSON.stringify({
        success: ok,
        status: status,
        url: HF_SPACE_URL,
        timestamp: new Date().toISOString(),
      }),
    };
  } catch (error) {
    console.error('❌ Ping failed:', error.message);
    
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message,
        url: HF_SPACE_URL,
        timestamp: new Date().toISOString(),
      }),
    };
  }
};
