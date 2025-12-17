import dotenv from "dotenv";
import Groq from "groq-sdk";

dotenv.config();


const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});


function getWeatherDetails(city = "") {
  const c = city.toLowerCase();

  if (c === "patiala") return "10°C";
  if (c === "mohali") return "15°C";
  if (c === "bangalore") return "23°C";
  if (c === "chandigarh") return "11°C";
  if (c === "delhi") return "16°C";

  return "Weather data not available";
}


const CITY_EXTRACT_PROMPT = `
You are an AI assistant.
Extract ONLY the city name from the user message.
Return the result strictly in JSON format.

Example:
User: What is the weather of Patiala?
Output:
{ "city": "Patiala" }
`;


const user = "Can you tell me the weather in Delhi today?";


async function chat() {
  console.log("STATE: START");
  console.log(user);

  const extractResponse = await groq.chat.completions.create({
    model: "llama-3.1-8b-instant",
    messages: [
      { role: "system", content: CITY_EXTRACT_PROMPT },
      { role: "user", content: user }
    ],
  });

  const rawText = extractResponse.choices[0].message.content;
  console.log("\nSTATE: CITY EXTRACT RAW");
  console.log(rawText);

  let city;
  try {
    city = JSON.parse(rawText).city;
  } catch (e) {
    console.log("Could not extract city");
    return;
  }

  console.log("\nSTATE: ACTION");
  console.log(`getWeatherDetails(city = "${city}")`);

  const weather = getWeatherDetails(city);
  console.log("\nSTATE: OBSERVATION");
  console.log(weather);

  console.log("\nSTATE: OUTPUT");
  console.log(` FINAL OUTPUT:\nWeather of ${city}: ${weather}`);
}

chat();
