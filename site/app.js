const filters = document.querySelectorAll(".filter");
const modules = document.querySelectorAll(".module-card");
const checkboxes = document.querySelectorAll("[data-progress]");
const progressLabel = document.querySelector("#progress-label");
const progressDetail = document.querySelector("#progress-detail");
const progressBar = document.querySelector("#progress-bar");
const storageKey = "ai-engineering-basics-progress";

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(storageKey) || "{}");
  } catch {
    return {};
  }
}

function writeProgress(progress) {
  localStorage.setItem(storageKey, JSON.stringify(progress));
}

function updateProgress() {
  const completed = Array.from(checkboxes).filter((checkbox) => checkbox.checked).length;
  const total = checkboxes.length;
  const percent = total === 0 ? 0 : Math.round((completed / total) * 100);

  progressLabel.textContent = `${percent}% complete`;
  progressDetail.textContent =
    completed === 0
      ? "No mastery tasks checked yet."
      : `${completed} of ${total} mastery tasks checked.`;
  progressBar.style.width = `${percent}%`;
}

function applyFilter(filterName) {
  modules.forEach((moduleCard) => {
    const categories = moduleCard.dataset.category || "";
    moduleCard.hidden = filterName !== "all" && !categories.includes(filterName);
  });
}

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filters.forEach((filter) => filter.classList.remove("active"));
    button.classList.add("active");
    applyFilter(button.dataset.filter);
  });
});

const progress = readProgress();
checkboxes.forEach((checkbox) => {
  const key = checkbox.dataset.progress;
  checkbox.checked = Boolean(progress[key]);
  checkbox.addEventListener("change", () => {
    const nextProgress = readProgress();
    nextProgress[key] = checkbox.checked;
    writeProgress(nextProgress);
    updateProgress();
  });
});

document.querySelectorAll(".copy-button").forEach((button) => {
  const originalText = button.textContent;
  button.addEventListener("click", async () => {
    const text = button.dataset.copy || "";
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = "Copied";
      setTimeout(() => {
        button.textContent = originalText;
      }, 1400);
    } catch {
      button.textContent = "Select text manually";
      setTimeout(() => {
        button.textContent = originalText;
      }, 1800);
    }
  });
});

updateProgress();
