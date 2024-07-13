document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('query-form');
    const queryInput = document.getElementById('query-input');
    const responseText = document.getElementById('response-text');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const query = queryInput.value;

        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            const data = await response.json();
            console.log(data);

            // Clear previous content
            responseText.innerHTML = '';

            // Display main message
            const mainMessage = document.createElement('p');
            mainMessage.textContent = data.message;
            responseText.appendChild(mainMessage);

            // Display events if available
            if (data.events && data.events.length > 0) {
                const eventsList = document.createElement('ul');
                data.events.forEach(event => {
                    const eventItem = document.createElement('li');
                    eventItem.innerHTML = `
                        <strong>${event.name}</strong><br>
                        <em>${event.start} - ${event.end}</em><br>
                        ${event.description}<br>
                        <a href="${event.url}" target="_blank">Ver más detalles</a>
                    `;
                    eventsList.appendChild(eventItem);
                });
                responseText.appendChild(eventsList);
            }

            // Display query for next month
            if (data.query_next_month) {
                const queryNextMonth = document.createElement('p');
                queryNextMonth.textContent = data.query_next_month;
                responseText.appendChild(queryNextMonth);
            }

            // Display exit message
            const exitMessage = document.createElement('p');
            exitMessage.textContent = data.exit_message;
            responseText.appendChild(exitMessage);

        } catch (error) {
            responseText.textContent = 'Error al obtener la respuesta';
        }
    });
});
