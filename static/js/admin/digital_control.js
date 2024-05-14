var product_number = 1

var product_mag = document.getElementById("product-mag").value;
var format = document.getElementById("format").value;
var ad_type = document.getElementById("ad-type").value;
var height = document.getElementById("height").value;
var width = document.getElementById("width").value;

function nextToSizeSetup() {
    product_mag = document.getElementById("product-mag").value;
    format = document.getElementById("format").value;
    ad_type = document.getElementById("ad-type").value;
    height = document.getElementById("height").value;
    width = document.getElementById("width").value;
    showHideStepModal('digital_product_step_size_setup', 'digital_product_step_product_info')
}

function createStandardSize() {
    var size_description = document.getElementById("size-description").value;
    var column_num = document.getElementById("column-num").value
    var size_height = document.getElementById("size-height").value
    console.log(size_description, size_height, column_num);
    newRow.innerHTML = `
    <td>${product_number + 1}</td>
    <td>${size_description}</td>
    <td>${column_num}</td>
    <td>${size_height}</td>
    <td>2.25</td>
    <td>
        <div class="switch2">
            <input id="status-toggle${product_number + 1}" class="check-toggle check-toggle-round-flat" type="checkbox" />
            <label for="status-toggle${product_number + 1}"></label>
            <span class="active">Active</span>
            <span class="deactivate">Deactivate</span>
        </div>
    </td>`;

    // Append the new row to the table body
    console.log(newRow);
    document.querySelector(".product-table tbody").appendChild(newRow);
    product_id = product_id + 1
}

// function reviewProduct() {
//     // document.getElementById("span_magazine_product").textContent = product_mag;
//     // document.getElementById("span_height").textContent = height;
//     // document.getElementById("span_width").textContent = width;
//     showHideStepModal('magazine_product_step_review', 'magazine_product_step_size_setup')
// }