var product_number = 1

var product_mag = document.getElementById("product-mag").value;
var measurement_type = document.getElementById("measurement-type").value;
var fold_orientation = document.getElementById("orientation").value;
var height = document.getElementById("height").value;
var width = document.getElementById("width").value;
var columns = document.getElementById("columns").value;
var column_width = document.getElementById("column-width").value;
var page_width = document.getElementById("page-width").value;
var page_height = document.getElementById("page-height").value;
var page_border = document.getElementById("page-border").value;
var gutter_size = document.getElementById("gutter-size").value;

function nextToSizeSetup() {
     product_mag = document.getElementById("product-mag").value;
     measurement_type = document.getElementById("measurement-type").value;
     fold_orientation = document.getElementById("orientation").value;
     height = document.getElementById("height").value;
     width = document.getElementById("width").value;
     columns = document.getElementById("columns").value;
     column_width = document.getElementById("column-width").value;
     page_width = document.getElementById("page-width").value;
     page_height = document.getElementById("page-height").value;
     page_border = document.getElementById("page-border").value;
     gutter_size = document.getElementById("gutter-size").value;
     showHideStepModal('magazine_product_step_size_setup', 'magazine_product_step_product_info')
}

function createStandardSize() {
     product_mag = document.getElementById("product-mag").value;
     measurement_type = document.getElementById("measurement-type").value;
     fold_orientation = document.getElementById("orientation").value;
     height = document.getElementById("height").value;
     width = document.getElementById("width").value;
     columns = document.getElementById("columns").value;
     column_width = document.getElementById("column-width").value;
     page_width = document.getElementById("page-width").value;
     page_height = document.getElementById("page-height").value;
     page_border = document.getElementById("page-border").value;
     gutter_size = document.getElementById("gutter-size").value;
    console.log(gutter_size);
    var size_description = document.getElementById("size-description").value;
    var column_num = document.getElementById("column-num").value
    var size_height = document.getElementById("size-height").value
    console.log(size_description, size_height, column_num);

    // Create a new table row
    var newRow = document.createElement("tr");

    // Populate the row with data
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
        </td>
    `;
    
    // Append the new row to the table body
    console.log(newRow);
    document.querySelector(".product-table tbody").appendChild(newRow);
    product_id = product_id + 1
}

function reviewProduct() {
    console.log(product_mag);
        document.getElementById("span_magazine_product").textContent = product_mag;
        document.getElementById("span_fold_orientation").textContent = fold_orientation;
        document.getElementById("span_height").textContent = height;
        document.getElementById("span_width").textContent = width;
        document.getElementById("span_columns").textContent = columns;
        document.getElementById("span_page_height").textContent = page_height;
        document.getElementById("span_page_border").textContent = page_border;
        document.getElementById("span_gutter_size").textContent = gutter_size;
        showHideStepModal('magazine_product_step_review', 'magazine_product_step_size_setup')
}

function getCookie(name) {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}

function submit() {
    let data = {
        product_mag : product_mag,
        measurement_type : measurement_type,
        fold_orientation : fold_orientation,
        height : height ? height : 0,
        width : width ? width : 0,
        columns : columns ? columns : 0,
        column_width : column_width ? column_width : 0,
        page_width : page_width ? page_width : 0,
        page_height : page_height ? page_height : 0,
        page_border : page_border ? page_border : 0,
        gutter_size : gutter_size ? gutter_size : 0,
    }
    fetch('/advertising/admin/financial/new-newspaper', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        $.toastr.success('Saved Success');
        showHideStepModal('magazine_product_step_success', 'magazine_product_step_review')
    })
    .catch(error => {
        $.toastr.error("Saved failure");
    });
}

