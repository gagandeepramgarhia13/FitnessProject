function capitalizeFirstLetter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function foodinfo() {
    const food_item = document.getElementById('food-name').value;
    const calories = document.getElementById('food-amount').value;

    fetch(`/food/get_food_info/${food_item}`, {})
        .then(response => response.json())
        .then(data => {
            food_api = data.food_api
            const table = document.createElement('table');
            const caption = document.createElement('caption');
            caption.textContent = `${capitalizeFirstLetter(food_api.name)}'s Nutrition details per ${food_api.serving_size_g}g`;
            table.appendChild(caption);

            const tbody = document.createElement('tbody');

            const createTableRow = (label, value) => {
                const row = document.createElement('tr');
                const labelCell = document.createElement('td');
                const valueCell = document.createElement('td');
                labelCell.textContent = label;
                valueCell.textContent = value;
                row.appendChild(labelCell);
                row.appendChild(valueCell);
                return row;
            };
            tbody.appendChild(
                createTableRow(
                    'Calories',
                    food_api.calories
                )
            );
            tbody.appendChild(createTableRow('Protein (g)', food_api.protein));
            tbody.appendChild(createTableRow('Carbohydrates Total (g)', food_api.carbs));

            tbody.appendChild(createTableRow('Fat Total (g)', food_api.fat));
            
            
            tbody.appendChild(createTableRow('Fibre (g)', food_api.fibre));


            table.appendChild(tbody);

            table.classList.add('table', 'table-bordered', 'table-striped', 'mx-auto', 'w-75');

            const foodDetailsDiv = document.getElementById('food-details');
            foodDetailsDiv.innerHTML = '';
            foodDetailsDiv.appendChild(table);

            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.classList.add('btn', 'btn-danger');
            removeButton.addEventListener('click', () => {
                foodDetailsDiv.innerHTML = '';
            });

            foodDetailsDiv.appendChild(removeButton);
        });
}