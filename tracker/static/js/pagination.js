function changePerPage(select) {
    const perPage = select.value;
    const currentUrl = new URL(window.location.href);

    // Update the "per_page" query parameter
    currentUrl.searchParams.set('per_page', perPage);
    currentUrl.searchParams.set('page', 1); // Reset to the first page

    // Reload the page with the updated URL
    window.location.href = currentUrl.toString();
}