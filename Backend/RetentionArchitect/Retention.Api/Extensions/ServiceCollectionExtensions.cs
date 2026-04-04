using Microsoft.Extensions.Options;
using Retention.Api.Models.Config;
using Retention.Api.Services;

namespace Retention.Api.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        services.AddHttpClient<MlServiceClient>((serviceProvider, client) =>
        {
            var options = serviceProvider
                .GetRequiredService<IOptions<MlServiceOptions>>()
                .Value;

            client.Timeout = TimeSpan.FromSeconds(options.TimeoutSeconds);
        });

        services.AddScoped<RecommendationService>();

        return services;
    }
}