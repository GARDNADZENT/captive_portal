function setPackage(packageValue, price) {
    // Set the hidden input values
    document.getElementById("priceInput").value = price;

    // Create and set the hidden input for package
    const packageInput = document.createElement("input");
    packageInput.type = "hidden";
    packageInput.name = "package";
    packageInput.value = packageValue;

    // Append to form and submit
    const form = document.getElementById("packageForm");
    form.appendChild(packageInput);
    form.submit();
}
