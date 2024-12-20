document.getElementById('risk-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('http://localhost:8000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('result').innerText = `Risk: ${result.risk}`;
        } else {
            throw new Error('Failed to fetch risk classification');
        }
    } catch (error) {
        console.error(error);
        document.getElementById('result').innerText = 'Error: Could not classify risk';
    }
});
