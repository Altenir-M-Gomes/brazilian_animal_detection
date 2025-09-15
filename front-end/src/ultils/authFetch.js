export async function authFetch(url, options) {
    const token = localStorage.getItem("token");

    const headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
    };

    const finalOptions = {
        ...options,
        headers,
    };

    const response = await fetch(url, finalOptions);

    if (response.status === 401) {
        window.location.href = "/login";
    }

    return response;
}