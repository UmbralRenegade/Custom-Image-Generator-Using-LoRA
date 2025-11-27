async function generate() {
    const prompt = document.getElementById("promptInput").value;

    const img = document.getElementById("result");
    img.src = "";
    img.alt = "Let him cook...";

    const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: prompt })
    });

    const data = await response.json();

    if (data.image) {
        img.src = "data:image/png;base64," + data.image;
        img.alt = "Generated image";
    } else {
        img.alt = "Error generating image";
        console.error("Backend error:", data);
    }
}
