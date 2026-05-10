from playwright.sync_api import sync_playwright


def get_section_text(page, heading_text: str) -> str:
    heading = page.locator(
        f"xpath=//*[normalize-space(.)='{heading_text}'][1]"
    )
    if heading.count() == 0:
        return ""

    heading = heading.first

    container = heading.locator("xpath=ancestor::section[1]")
    if container.count() == 0:
        container = heading.locator("xpath=ancestor::div[1]")
    if container.count() == 0:
        return ""

    container = container.first

    read_more = container.locator(
        "xpath=.//a[contains(., 'Read more') or contains(., 'Show more') or contains(., 'More')]"
        " | .//button[contains(., 'Read more') or contains(., 'Show more') or contains(., 'More')]"
    )

    if read_more.count() > 0:
        try:
            read_more.first.click(timeout=2000)
            page.wait_for_timeout(300)
        except:
            pass

    try:
        text = container.inner_text().strip()
    except:
        return ""

    parts = text.split(heading_text, 1)
    if len(parts) == 2:
        text = parts[1].strip()

    return text


def scrape_profile(url: str) -> dict:
    base = url.rstrip("/")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(base + "/about", wait_until="domcontentloaded", timeout=60000)
        except:
            page.goto(base, wait_until="domcontentloaded", timeout=60000)

        page.wait_for_load_state("networkidle")

        name = page.locator("h1").first.text_content()
        name = name.strip() if name else ""

        bio = get_section_text(page, "BIO")
        fields = get_section_text(page, "FIELDS OF RESEARCH")

        def get_research_interests():
            candidates = [
                base + "/research",
                base + "/research-interests",
                base + "/grants",
                base + "/publications",
                base + "/about",
            ]

            for u in candidates:
                try:
                    page.goto(u, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_load_state("networkidle")

                    text = (
                        get_section_text(page, "RESEARCH INTERESTS")
                        or get_section_text(page, "Research interests")
                        or get_section_text(page, "Research Interests")
                    )

                    if text.strip():
                        return text.strip()

                except:
                    continue

            return ""

        research_interests = get_research_interests()

        browser.close()

    return {
        "name": name,
        "bio": bio,
        "fields": fields,
        "research_interests": research_interests,
    }