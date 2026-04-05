using Microsoft.AspNetCore.Mvc;
using Retention.Api.Models.Requests;

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

    [HttpGet("user")]
    public IActionResult PredictUser([FromBody] PredictUserRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.UserId))
        {
            return BadRequest("UserId is required.");
        }

        return Ok(new
        {
            userId = request.UserId,
            message = "Prediction endpoint works."
        });
    }
}
