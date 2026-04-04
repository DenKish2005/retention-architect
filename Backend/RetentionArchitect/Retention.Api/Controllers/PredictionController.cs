using Microsoft.AspNetCore.Mvc;
using Retention.Api.Models.Requests;
using Retention.Api.Services;

namespace Retention.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionController : ControllerBase
{
    private readonly MlServiceClient mlServiceClient;
    private readonly RecommendationService recommendationService;

    public PredictionController(
        MlServiceClient mlServiceClient,
        RecommendationService recommendationService)
    {
        this.mlServiceClient = mlServiceClient;
        this.recommendationService = recommendationService;
    }

    [HttpGet("health")]
    public IActionResult Health()
    {
        return Ok("Retention API is running.");
    }

    [HttpGet("health/ml")]
    public async Task<IActionResult> HealthMl()
    {
        var ok = await mlServiceClient.HealthAsync();

        if (!ok)
        {
            return StatusCode(503, "ML service is unavailable.");
        }

        return Ok("ML service is running.");
    }

    [HttpPost("user")]
    public async Task<IActionResult> PredictUser([FromBody] PredictUserRequest request)
    {
        if (request is null || string.IsNullOrWhiteSpace(request.UserId))
        {
            return BadRequest("UserId is required.");
        }

        var result = await mlServiceClient.PredictUserAsync(request);

        if (result is null)
        {
            return StatusCode(502, "ML service returned no response.");
        }

        if (result.RecommendedActions is null || result.RecommendedActions.Count == 0)
        {
            result.RecommendedActions = recommendationService.BuildFallbackRecommendations(result);
        }

        return Ok(result);
    }

    [HttpPost("batch")]
    public async Task<IActionResult> PredictBatch([FromBody] PredictBatchRequest request)
    {
        if (request is null || request.UserIds is null || request.UserIds.Count == 0)
        {
            return BadRequest("At least one userId is required.");
        }

        var result = await mlServiceClient.PredictBatchAsync(request);

        if (result is null)
        {
            return StatusCode(502, "ML service returned no response.");
        }

        foreach (var prediction in result)
        {
            if (prediction.RecommendedActions is null || prediction.RecommendedActions.Count == 0)
            {
                prediction.RecommendedActions = recommendationService.BuildFallbackRecommendations(prediction);
            }
        }

        return Ok(result);
    }
}