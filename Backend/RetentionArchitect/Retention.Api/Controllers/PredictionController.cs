using Microsoft.AspNetCore.Mvc;
using Retention.Api.Models.Requests;
using Retention.Api.Services;

namespace Retention.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionController : ControllerBase
{
    [HttpGet("health")]
    public IActionResult Health()
    {
        return Ok("Retention API is running.");
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
