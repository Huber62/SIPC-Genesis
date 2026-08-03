async function initialize() {
    const status = document.getElementById("status");
    const modules = document.getElementById("modules");

    try {
        const healthResponse = await fetch("/api/health");
        const health = await healthResponse.json();

        const systemResponse = await fetch("/api/system");
        const system = await systemResponse.json();

        status.textContent = health.status === "ok"
            ? "Sistema operativo"
            : "Sistema non disponibile";

        modules.innerHTML = system.modules
            .map((module) => `<div class="module">${module}</div>`)
            .join("");
    } catch (error) {
        status.textContent = "Errore di collegamento";
        console.error(error);
    }
}

initialize();
