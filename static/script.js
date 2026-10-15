document.addEventListener("DOMContentLoaded", function () {
    const choiceForms = document.querySelectorAll(".choice-form");

    choiceForms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector("button");

            if (!button || button.disabled) {
                return;
            }

            button.classList.add("is-selected");
            button.disabled = true;

            choiceForms.forEach(function (otherForm) {
                const otherButton = otherForm.querySelector("button");
                if (otherButton && otherButton !== button) {
                    otherButton.disabled = true;
                }
            });
        });
    });

    const story = document.querySelector(".story-text");
    const revealButton = document.querySelector(".reveal-story");
    const reduceMotion = window.matchMedia
        && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (!story || !revealButton || reduceMotion) {
        return;
    }

    const fullText = story.textContent;
    const characters = Array.from(fullText);
    let characterIndex = 0;
    let typingTimer;

    revealButton.hidden = false;
    story.textContent = "";
    story.classList.add("is-typing");

    function typeNextCharacter() {
        if (characterIndex >= characters.length) {
            story.classList.remove("is-typing");
            revealButton.hidden = true;
            return;
        }

        story.textContent += characters[characterIndex];
        characterIndex += 1;
        typingTimer = window.setTimeout(typeNextCharacter, 24);
    }

    revealButton.addEventListener("click", function () {
        window.clearTimeout(typingTimer);
        story.textContent = fullText;
        story.classList.remove("is-typing");
        revealButton.hidden = true;
    });

    typeNextCharacter();
});
