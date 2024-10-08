async function view(id) {
  try {
    await fetch(`/user/${id}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        try {
          if (data) {
            const user = data;

            const userContainer = document.getElementById("user-view");
            if (!userContainer) {
              throw new Error("User view container not found");
            }

            userContainer.innerHTML = `
          <div class="flex justify-between items-center mb-6">
            <div class="text-left">
              <h5 class="h5 font-semibold">User</h5>
              <h6 class="h6 font-normal">On Ecosystem</h6>
            </div>
            <div class="flex items-center">
              <button
                type="button"
                class="btn h5 font-semibold bg-blue-400"
                onclick="back()"
              >
                Back
              </button>
            </div>
          </div>
    
          <div class="flex mt-6">
            <div
              class="grid grid-cols-2 gap-4 mx-auto p-4 to-base-200 shadow rounded-xl"
            >
              <div class="col-span-2 flex justify-center">
                <img
                  src=${user.profile}
                  alt="profile photo"
                  class="w-24 h-24 rounded-full object-cover border-2 ${
                    user.profile ? "border-green-400" : "border-red-400"
                  }"
                  onerror="this.src='/static/images/profile.png';"
                />
              </div>
              <p class="font-medium">Username:</p>
              <p>${user.username || "N/A"}</p>
              <p class="font-medium">Email:</p>
              <p>${user.email || "N/A"}</p>
              <p class="font-medium">First Name:</p>
              <p>${user.first_name || "N/A"}</p>
              <p class="font-medium">Last Name:</p>
              <p>${user.last_name || "N/A"}</p>
              <p class="font-medium">Country:</p>
              <p>${user.country || "N/A"}</p>
              <p class="font-medium">Date of Birth:</p>
              <p>${user.dob || "N/A"}</p>
              <p class="font-medium">Verified:</p>
              <p class="${user.verified ? "text-green-500" : "text-red-500"}">${
              user.verified ? "Yes" : "No"
            }</p>
              <p class="font-medium">Mobile Number:</p>
              <p>${user.mobile || "N/A"}</p>
            </div>
          </div>
        `;

            const usersView = document.querySelector("#users-view");
            if (usersView) {
              usersView.style.display = "none";
            }
            userContainer.style.display = "block";
          }
        } catch (error) {
          console.error("Error fetching and displaying users:", error);
        }
      });
  } catch (error) {
    console.error("Error in view function:", error);
    alert(
      "An error occurred while displaying user information. Please try again."
    );
  }
}

function back() {
  const usersView = document.querySelector("#users-view");
  const userView = document.querySelector("#user-view");

  if (usersView && userView) {
    usersView.style.display = "block";
    userView.style.display = "none";
  } else {
    console.error("Required view elements not found");
  }
}
