using Microsoft.AspNetCore.Mvc;
using Retention.Api.Models.Requests;
using Retention.Api.Services;

namespace Retention.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionController : ControllerBase
{
    [HttpGet("health/ml")]
    public async Task<IActionResult> HealthMl()
    {
        var ok = await mlServiceClient.HealthAsync();
        if (!ok)
            return StatusCode(503, "ML service is unavailable.");

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

        return Ok(result);
    }

    private readonly MlServiceClient mlServiceClient;

    public PredictionController(MlServiceClient mlServiceClient)
    {
        this.mlServiceClient = mlServiceClient;
    }
}
