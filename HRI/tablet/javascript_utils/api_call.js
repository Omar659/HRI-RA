class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async call(method, endpoint, data = null, params = null) {
        const url = `${this.baseURL}${endpoint}${params ? `?${new URLSearchParams(params).toString()}` : ''}`;
        console.log(url)
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": this.baseURL
            },
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.message || 'Errore nella chiamata API');
            }

            return responseData;
        } catch (error) {
            throw error;
        }
    }

    async get(endpoint, params) {
        return await this.call('GET', endpoint, null, params);
    }

    async post(endpoint, data, params) {
        return await this.call('POST', endpoint, data, params);
    }

    async put(endpoint, data, params) {
        return await this.call('PUT', endpoint, data, params);
    }

    async delete(endpoint, params) {
        return await this.call('DELETE', endpoint, null, params);
    }
}