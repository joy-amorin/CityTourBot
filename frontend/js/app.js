document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('query-form')
    const queryInput = document.getElementById('query-input')
    const responseText = document.getElementById('response-text')

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const query = queryInput.value;

        try{
            const response = await fetch('http://127.0.0.1:8000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });
            const data = await response.json();
            console.log(data);
            responseText.textContent = data.response;
        }catch (error) {
            responseText.textContent = 'Error al obtener la repuesta'
        }
    });
});