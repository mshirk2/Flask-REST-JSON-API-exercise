const BASE_URL = "http://localhost:5000/api";

function generateHTML(cupcake) {
    return `
        <div data-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-btn>X</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}" alt="(no image provided)">
        </div>`;
}


async function showInitialCupcakes(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


$("#add-cupcake").on("submit", async function(evt){
    evt.preventDefault();

    let flavor = $("#flavor-input").val();
    let rating = $("#rating-input").val();
    let size = $("#size-input").val();
    let image = $("#image-input").val();

    const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {flavor, rating, size, image});

    let newCupcake = $(generateHTML(newCupcakeResp.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#add-cupcake").trigger("reset");
});


$("#cupcakes-list").on("click", ".delete-btn", async function(evt){
    evt.preventDefault();

    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showInitialCupcakes);