const PRECO = 20;
let selecionados = [];

function toggleNumero(num, el) {
    if (el.classList.contains("ativo")) {
        el.classList.remove("ativo");
        selecionados = selecionados.filter(n => n !== num);
    } else {
        el.classList.add("ativo");
        selecionados.push(num);
    }
    atualizarResumo();
}

function atualizarResumo() {
    document.getElementById("qtdNumeros").innerText = selecionados.length;
    document.getElementById("valorTotal").innerText =
        (selecionados.length * PRECO).toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });
}

function confirmar() {
    const nome = document.getElementById("nome").value;
    const cpf = document.getElementById("cpf").value;
    const celular = document.getElementById("celular").value;

    if (!nome || !cpf || !celular || selecionados.length === 0) {
        alert("Preencha seus dados e selecione ao menos um número");
        return;
    }

    fetch("/reservar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome,
            cpf,
            celular,
            numeros: selecionados
        })
    }).then(() => {
        const msg = `Olá! Comprei ${selecionados.length} número(s) na Rifa do Theo.`;
        window.open(
            `https://wa.me/5548988192173?text=${encodeURIComponent(msg)}`
        );
        location.reload();
    });
}
