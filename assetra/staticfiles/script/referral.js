async function view(referral) {
  const referralContainer = document.getElementById("referral-view");
  referralContainer.innerHTML = "";

  referralContainer.innerHTML = `
        <div class="flex justify-between items-center mb-6">
            <div class="text-left">
                <h5 class="h5 font-semibold">Referral</h5>
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
      `;

  document.querySelector("#referrals-view").style.display = "none";
  document.querySelector("#referral-view").style.display = "block";
}

async function back() {
  document.querySelector("#referral-view").style.display = "none";
  document.querySelector("#referrals-view").style.display = "block";
}
