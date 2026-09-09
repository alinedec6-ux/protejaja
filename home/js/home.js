document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".alert").forEach((alerta) => {
        window.setTimeout(() => {
            alerta.style.transition = "opacity 0.4s ease";
            alerta.style.opacity = "0";
            window.setTimeout(() => alerta.remove(), 400);
        }, 6000);
    });

    const anexo = document.getElementById("anexo");
    const preview = document.getElementById("preview-anexo");

    if (anexo && preview) {
        anexo.addEventListener("change", () => {
            preview.innerHTML = "";
            preview.classList.add("hidden");

            const arquivo = anexo.files[0];
            if (!arquivo) return;

            preview.classList.remove("hidden");
            const info = document.createElement("p");
            info.className = "text-xs text-slate-600";

            if (arquivo.type.startsWith("image/")) {
                const img = document.createElement("img");
                img.src = URL.createObjectURL(arquivo);
                img.className = "w-32 h-32 object-cover rounded-xl border border-rose-100 mb-2";
                preview.appendChild(img);
                info.textContent = arquivo.name + " (" + Math.round(arquivo.size / 1024) + " KB)";
            } else {
                info.textContent = "📎 " + arquivo.name + " (" + Math.round(arquivo.size / 1024) + " KB)";
            }

            preview.appendChild(info);
        });
    }
});