async function loadDaily() {
    const today = new Date().toISOString().split("T")[0];
    const url = `data/daily_tests/${today}/daily_test.json`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        const list = document.getElementById("daily-list");
        list.innerHTML = "";
        data.forEach((q,i) => {
            const li = document.createElement("li");
            li.textContent = q.question;
            li.onclick = () => showContent(q);
            list.appendChild(li);
        });
    } catch(e) {
        console.log("No daily test yet.");
    }
}

function showContent(q) {
    const div = document.getElementById("content");
    div.innerHTML = `<h3>${q.question}</h3>
    <ul>${q.options.map(opt => `<li>${opt} - ${q.notes[opt]}</li>`).join('')}</ul>
    <p>Answer: ${q.answer}</p>`;
}

loadDaily();
