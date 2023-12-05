// Function to update parent checkbox state based on child checkboxes
function updateParentCheckbox(childCheckboxes, parentCheckbox) {
    let allChecked = true;
    for (const checkbox of childCheckboxes) {
        if (!checkbox.checked) {
            allChecked = false;
            break;
        }
    }
    parentCheckbox.checked = allChecked;
}

const OrganizationCheckbox = document.getElementById("Organization");
const OrganizationChildCheckboxes = document.querySelectorAll(".Organization");

// Event listener for parent checkbox
OrganizationCheckbox.addEventListener("change", function () {
    for (const checkbox of OrganizationChildCheckboxes) {
        checkbox.checked = OrganizationCheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of OrganizationChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(OrganizationChildCheckboxes, OrganizationCheckbox);
    });
}

const QECheckbox = document.getElementById("QE");
const QEChildCheckboxes = document.querySelectorAll(".QE");

// Event listener for parent checkbox
QECheckbox.addEventListener("change", function () {
    for (const checkbox of QEChildCheckboxes) {
        checkbox.checked = QECheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of QEChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(QEChildCheckboxes, QECheckbox);
    });
}

const TestDataCheckbox = document.getElementById("Test_Data");
const TestDataChildCheckboxes = document.querySelectorAll(".Test_Data");

// Event listener for parent checkbox
TestDataCheckbox.addEventListener("change", function () {
    for (const checkbox of TestDataChildCheckboxes) {
        checkbox.checked = TestDataCheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of TestDataChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(TestDataChildCheckboxes, TestDataCheckbox);
    });
}

const TestEnvCheckbox = document.getElementById("TestEnv");
const TestEnvChildCheckboxes = document.querySelectorAll(".TestEnv");

// Event listener for parent checkbox
TestEnvCheckbox.addEventListener("change", function () {
    for (const checkbox of TestEnvChildCheckboxes) {
        checkbox.checked = TestEnvCheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of TestEnvChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(TestEnvChildCheckboxes, TestEnvCheckbox);
    });
}

const SpecializationCheckbox = document.getElementById("Specialization");
const SpecializationChildCheckboxes = document.querySelectorAll(".Specialization");

// Event listener for parent checkbox
SpecializationCheckbox.addEventListener("change", function () {
    for (const checkbox of SpecializationChildCheckboxes) {
        checkbox.checked = SpecializationCheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of SpecializationChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(SpecializationChildCheckboxes, SpecializationCheckbox);
    });
}

const DevOpsCheckbox = document.getElementById("DevOps");
const DevOpsChildCheckboxes = document.querySelectorAll(".DevOps");

// Event listener for parent checkbox
DevOpsCheckbox.addEventListener("change", function () {
    for (const checkbox of DevOpsChildCheckboxes) {
        checkbox.checked = DevOpsCheckbox.checked;
    }
});

// Event listener for child checkboxes
for (const checkbox of DevOpsChildCheckboxes) {
    checkbox.addEventListener("change", function () {
        updateParentCheckbox(DevOpsChildCheckboxes, DevOpsCheckbox);
    });
}