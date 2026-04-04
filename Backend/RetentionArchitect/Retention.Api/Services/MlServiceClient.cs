using System.Net.Http.Json;
using Microsoft.Extensions.Options;
using Retention.Api.Models.Config;
using Retention.Api.Models.Requests;
using Retention.Api.Models.Responses;

namespace Retention.Api.Services;

public class MlServiceClient
{
    private readonly HttpClient httpClient;
    private readonly MlServiceOptions options;

    public MlServiceClient(HttpClient httpClient, IOptions<MlServiceOptions> options)
    {
        this.httpClient = httpClient;
        this.options = options.Value;
    }

    public async Task<PredictionResponse?> PredictUserAsync(PredictUserRequest request)
    {
        try
        {
            var url = $"{options.BaseUrl}/predict_user";
            var response = await httpClient.PostAsJsonAsync(url, request);

            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            return await response.Content.ReadFromJsonAsync<PredictionResponse>();
        }
        catch
        {
            return null;
        }
    }

    public async Task<List<PredictionResponse>?> PredictBatchAsync(PredictBatchRequest request)
    {
        try
        {
            var url = $"{options.BaseUrl}/predict_batch";
            var response = await httpClient.PostAsJsonAsync(url, request);

            if (!response.IsSuccessStatusCode)
            {
                return null;
            }

            return await response.Content.ReadFromJsonAsync<List<PredictionResponse>>();
        }
        catch
        {
            return null;
        }
    }

    public async Task<bool> HealthAsync()
    {
        try
        {
            var response = await httpClient.GetAsync($"{options.BaseUrl}/health");
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }
}